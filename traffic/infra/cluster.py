from traffic.infra.interfaces.cluster_interface import ClusterInterface
from shapely.geometry import MultiPoint
import hdbscan
import pandas as pd


class Cluster(ClusterInterface):
    def _calculate_centroid(self, df, cluster):
        cluster_df = df.pipe(lambda x: x[x.cluster == cluster])
        x_values = cluster_df.x
        y_values = cluster_df.y

        points = zip(x_values, y_values)
        multi_points = MultiPoint(list(points))

        return multi_points.centroid

    def clusterize(self, points_info_dict, points_to_cluster, top_jams):
        points_info = pd.DataFrame(
            points_info_dict,
            columns=[
                "point_incident_length",
                "point_incident_delay",
                "points_incident_datetime",
            ],
        )
        df = pd.DataFrame(points_to_cluster)
        clusterer = hdbscan.HDBSCAN(min_cluster_size=30)
        clusterer.fit(df)
        labels = pd.Series(clusterer.labels_, index=df.index, name="cluster")
        labels_df = pd.DataFrame(labels)

        points_per_cluster = (
            labels_df.pipe(lambda x: x[x.cluster >= 0])
            .assign(point_id=lambda x: x.index)
            .merge(df, left_index=True, right_index=True)
        )

        top_clusters = labels[labels >= 0].value_counts().head(top_jams).index

        top_center_points = []

        for cluster in top_clusters:
            top_center_points.append(
                self._calculate_centroid(points_per_cluster, cluster)
            )

        top_center_points_x = []
        top_center_points_y = []

        for point in top_center_points:
            top_center_points_x.append(point.x)
            top_center_points_y.append(point.y)

        top_clusters_df = pd.DataFrame(top_clusters, columns=["cluster"]).assign(
            points=list(zip(top_center_points_x, top_center_points_y))
        )

        top_clusters_point_info_df = (
            points_per_cluster[points_per_cluster.cluster.isin(top_clusters)]
            .merge(points_info, left_on="point_id", right_index=True)
            .merge(top_clusters_df, left_on="cluster", right_on="cluster", how="left")
        )

        max_delay_points_id_list = (
            top_clusters_point_info_df.groupby("cluster")["point_incident_delay"]
            .idxmax()
            .tolist()
        )

        max_delay_points_info_df = top_clusters_point_info_df.pipe(
            lambda x: x[x.index.isin(max_delay_points_id_list)]
        )

        return max_delay_points_info_df
