def build_work_names(results, works_dict):
    return sorted(
        {
            works_dict.get(str(result["work_id"])).work_name
            for result in results
            if str(result.get("work_id")) in works_dict
        }
    )
