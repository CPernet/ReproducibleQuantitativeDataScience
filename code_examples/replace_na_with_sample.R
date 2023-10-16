#' Replace NA values in a data frame with sample values.
#'
#' This function replaces NA values in a given data frame `p` with
#' random sample values taken from another reference data frame `prices_complete`.
#' The sampling is based on matching "EANcode" values between the two data frames.
#'
#' @param p A data frame with potential NA values that need replacement.
#' @param prices_complete A reference list of data frames, named by "EANcode",
#'                        from which sample values are drawn to replace the NAs in `p`.
#'
#' @return A data frame with the same structure as `p` but with NA values replaced.
#'
#' @examples
#' # Assuming 'df_with_na' is your data with NAs and 'prices_reference' is your reference list
#' df_filled <- replace_na_with_sample(df_with_na, prices_reference)
#'
replace_na_with_sample <- function(p, prices_complete) {
    # Function to replace NA for a given row
    replace_row_na <- function(row) {
        eancode <- row["EANcode"]

        # If the EANcode is in prices_complete
        if (eancode %in% names(prices_complete)) {
            df <- prices_complete[[as.character(eancode)]]

            # For each NA value in the row, replace with a random sample from df$price
            na_indices <- is.na(row)
            row[na_indices] <- sample(df$price, sum(na_indices), replace = TRUE)
        }

        return(row)
    }

    # Identify numeric columns in the original dataframe
    numeric_cols <- colnames(p)[sapply(p, is.numeric)]

    # Apply the function to each row of p
    p_new <- as.data.frame(t(apply(p, 1, replace_row_na)))

    # Set the column names of p_new to be the same as p
    colnames(p_new) <- colnames(p)

    # Convert the identified numeric columns back to numeric type in p_new
    p_new[numeric_cols] <- lapply(p_new[numeric_cols], as.numeric)

    return(p_new)
}