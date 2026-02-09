def extract_work_names(results, works_dict):
    return sorted(
        {
            str(works_dict[str(result["work_id"])])
            for result in results
            if str(result.get("work_id")) in works_dict
        }
    )
