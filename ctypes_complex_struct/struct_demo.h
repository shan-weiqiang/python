#ifndef STRUCT_DEMO_H
#define STRUCT_DEMO_H

#define MAX_METRICS   4
#define MAX_TAGS      4
#define MAX_WEIGHTS   8
#define MAX_LABEL     32
#define MAX_SUMMARY   3
#define MAX_PTRS      2

typedef struct {
    int x;
    int y;
} Point;

typedef struct {
    char  label[MAX_LABEL];
    int   weight;
    Point anchor;
} Metric;

typedef struct {
    char   header_id[MAX_LABEL];
    int    version;
    Point  origin;
    Point  corners[2];
    Metric metrics[MAX_METRICS];
    int    weights[MAX_WEIGHTS];
    char   categories[MAX_TAGS][MAX_LABEL];
    char  *description;
    char  *tags[MAX_TAGS];
    int    tag_count;
    Metric *metric_ptrs[MAX_PTRS];
    int    metric_ptr_count;
} InputRecord;

typedef struct {
    char   title[MAX_LABEL];
    Point  bbox[2];
    int    total_weight;
    int    filtered_weights[MAX_WEIGHTS];
    int    filtered_weight_count;
    Metric top_metrics[MAX_PTRS];
    char   summary_lines[MAX_SUMMARY][MAX_LABEL];
    char  *notes;
    Metric *ranked_ptrs[MAX_PTRS];
    int    ranked_ptr_count;
} OutputRecord;

OutputRecord transform_record(
    const InputRecord *input,
    double scale,
    int min_weight,
    int top_n
);

void free_output_record(OutputRecord *output);

#endif /* STRUCT_DEMO_H */
