kwh_total_value_start_str = '1.8.0('
kwh_t1_value_start_str = '1.8.1('
kwh_t2_value_start_str = '1.8.2('
kwh_value_end_str = '*kWh'


def get_kwh_values(data_str):

    """ return kwh values from input data
    :arg data_str .. tariff message body (string)
    :return kwh values: total, t1, t2 """

    tot_begin = data_str.find(kwh_total_value_start_str) + len(kwh_total_value_start_str)
    tot_end = tot_begin + data_str[tot_begin:].find(kwh_value_end_str)
    t1_begin = tot_end + data_str[tot_end:].find(kwh_t1_value_start_str) + len(kwh_t1_value_start_str)
    t1_end = t1_begin + data_str[t1_begin:].find(kwh_value_end_str)
    t2_begin = t1_end + data_str[t1_end:].find(kwh_t2_value_start_str) + len(kwh_t2_value_start_str)
    t2_end = t2_begin + data_str[t2_begin:].find(kwh_value_end_str)

    tot_kwh = data_str[tot_begin:tot_end]
    t1_kwh = data_str[t1_begin:t1_end]
    t2_kwh = data_str[t2_begin:t2_end]

    return float(tot_kwh), float(t1_kwh), float(t2_kwh)


