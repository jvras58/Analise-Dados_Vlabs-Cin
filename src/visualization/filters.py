# Filter Data
def apply_filters(df, movement_filter, complexity_filter):
    if movement_filter:
        df = df[df['movement_detail'].isin(movement_filter)]
    if complexity_filter:
        df = df[df['complexity'].isin(complexity_filter)]
    return df