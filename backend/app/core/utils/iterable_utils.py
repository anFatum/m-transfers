def check_missing(set_to_check, set_compare_with):
    missing_params = [param for param in set_compare_with
                      if param not in set_to_check or not set_to_check[param]]
    return missing_params


def delete_none_keys(dict_to_clean: dict) -> dict:
    return {k: v for k, v in dict_to_clean.items() if v is not None}
