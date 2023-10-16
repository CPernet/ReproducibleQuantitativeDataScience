def perform_lof(df, reduced_data, contamination=contamination, lof_abod_neighbors=lof_abod_neighbors, metric='euclidean', col_name='lof_outliers'):
    tic = time.perf_counter()

    lof = LocalOutlierFactor(n_neighbors=lof_abod_neighbors, contamination=contamination, metric=metric)
    y_pred = lof.fit_predict(reduced_data)
    df[col_name] = y_pred
    df[col_name].replace([-1, 1], [1,0], inplace=True)

    toc = time.perf_counter()
    print(f"LOF took {(toc - tic)/60} minutes")