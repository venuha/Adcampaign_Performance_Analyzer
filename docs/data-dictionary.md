# Campaign CSV data dictionary

The dataset has one row per **campaign ID per reporting day**. Monetary values
are in USD. Dates are inclusive when filtering.

| Column | Type | Meaning and validation |
| --- | --- | --- |
| `date` | Date | Valid reporting date in YYYY-MM-DD format |
| `campaign_id` | Text | Nonblank campaign identifier; preserved as text on CSV load |
| `campaign_name` | Text | Nonblank campaign label |
| `platform` | Text | Nonblank advertising channel |
| `audience` | Text | Nonblank audience segment |
| `campaign_goal` | Text | Nonblank objective |
| `impressions` | Integer | Nonnegative number of ad views |
| `clicks` | Integer | Nonnegative tracked clicks, no greater than impressions |
| `conversions` | Integer | Nonnegative tracked actions, no greater than clicks |
| `spend` | Number | Finite, nonnegative ad spend in USD |
| `revenue` | Number | Finite, nonnegative attributed revenue in USD |

Each ID must retain the same name, platform, audience, and goal across dates.
Duplicate date/ID combinations are rejected. Required values cannot be
missing. Additional columns are ignored. Validation returns a sorted copy
without modifying the original input DataFrame.

## Attribution assumptions

The conversion validation assumes at most one tracked action per click.
Real exports that include view-through conversions or multiple actions per
click require a deliberate change to that rule before analysis.
Use one currency and consistent attribution windows, reporting timezones, and
deduplicated conversions across uploaded rows.

Sample Sales conversions represent purchases. Lead Generation conversions
represent leads, and Brand Awareness conversions represent engagement
actions. Only Sales campaigns have attributed revenue. The fictional sample
includes paused days and zero-conversion days.

## Time aggregation

Daily periods use the reporting day. Weeks start Monday. Monthly periods use
the first day of the calendar month. Filters apply before aggregation, so
boundary weeks and months contain only the dates selected. Missing periods
represent no recorded data; the application does not manufacture zero rows.
