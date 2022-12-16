from config import CLUSTER_LIST
from functions import get_saved_objects, get_object_query, write_to_csv, get_region, get_account_id, is_heavy
from SavedObject import Dashboard, Visualization, Search


def main():
    problematic_objects = []

    for cluster in CLUSTER_LIST:
        print(f"Started collecting data from cluster {cluster}")
        saved_objects = get_saved_objects(cluster)

        region = get_region(cluster)

        if saved_objects:
            for saved_object in saved_objects:
                object_source = saved_object.get("_source")
                object_type = object_source.get("type")

                if object_type == "dashboard":
                    object_json = object_source.get("dashboard")

                elif object_type == "visualization":
                    object_json = object_source.get("visualization")

                else:  # object_type == "search":
                    object_json = object_source.get("search")

                query, filters = get_object_query(object_json)
                heavy, problematic_query, problematic_filters = is_heavy(query, filters)

                if heavy:
                    object_full_id = saved_object.get("_id")
                    object_references = object_source.get("references")

                    if object_type == "dashboard":
                        kibana_index = saved_object.get("_index")
                        saved_obj = Dashboard(object_json, object_references, object_full_id, kibana_index)

                    elif object_type == "visualization":
                        saved_obj = Visualization(object_json, object_references, object_full_id)

                    else:  # object_type == "search":
                        saved_obj = Search(object_json, object_references, object_full_id)

                    account_id = get_account_id(region, saved_obj.index)

                    problematic_objects.append({"Account id": account_id,
                                                           "Company Name": saved_obj.company,
                                                           "Region": region,
                                                           "Cluster": cluster,
                                                           "Saved Object Type": object_type,
                                                           "Name": saved_obj.name,
                                                           "Object id": saved_obj.object_id,
                                                           "Last Updated At": saved_obj.last_updated,
                                                           "Problematic Query": problematic_query,
                                                           "Problematic Filters": problematic_filters})
    print("Finished collecting data, writing found info to CSV.")
    write_to_csv(problematic_objects)


if __name__ == '__main__':
    main()
