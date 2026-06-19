#include "struct_demo.h"

#include <stdlib.h>
#include <string.h>
#include <stdio.h>

static void copy_metric(Metric *dst, const Metric *src)
{
    memcpy(dst->label, src->label, MAX_LABEL);
    dst->weight = src->weight;
    dst->anchor = src->anchor;
}

static int compare_metric_weight(const void *a, const void *b)
{
    const Metric *left = *(const Metric * const *)a;
    const Metric *right = *(const Metric * const *)b;
    return right->weight - left->weight;
}

OutputRecord transform_record(
    const InputRecord *input,
    double scale,
    int min_weight,
    int top_n
)
{
    OutputRecord output;
    memset(&output, 0, sizeof(output));

    snprintf(output.title, MAX_LABEL, "%s@v%d", input->header_id, input->version);

    output.bbox[0] = input->corners[0];
    output.bbox[1] = input->corners[1];

    for (int i = 0; i < MAX_WEIGHTS; ++i) {
        int scaled = (int)(input->weights[i] * scale);
        output.total_weight += scaled;
        if (input->weights[i] >= min_weight) {
            output.filtered_weights[output.filtered_weight_count++] = scaled;
        }
    }

    Metric candidates[MAX_METRICS * 2];
    int candidate_count = 0;

    for (int i = 0; i < MAX_METRICS && candidate_count < MAX_METRICS * 2; ++i) {
        if (input->metrics[i].label[0] != '\0') {
            candidates[candidate_count++] = input->metrics[i];
        }
    }
    for (int i = 0; i < input->metric_ptr_count && candidate_count < MAX_METRICS * 2; ++i) {
        if (input->metric_ptrs[i] != NULL) {
            candidates[candidate_count++] = *input->metric_ptrs[i];
        }
    }

    Metric *sorted[MAX_METRICS * 2];
    for (int i = 0; i < candidate_count; ++i) {
        sorted[i] = &candidates[i];
    }
    qsort(sorted, candidate_count, sizeof(Metric *), compare_metric_weight);

    if (top_n > MAX_PTRS) {
        top_n = MAX_PTRS;
    }
    if (top_n > candidate_count) {
        top_n = candidate_count;
    }

    output.ranked_ptr_count = top_n;
    for (int i = 0; i < top_n; ++i) {
        copy_metric(&output.top_metrics[i], sorted[i]);
        output.ranked_ptrs[i] = (Metric *)malloc(sizeof(Metric));
        copy_metric(output.ranked_ptrs[i], sorted[i]);
    }

    for (int i = 0; i < MAX_SUMMARY && i < input->tag_count; ++i) {
        if (input->tags[i] != NULL) {
            strncpy(output.summary_lines[i], input->tags[i], MAX_LABEL - 1);
            output.summary_lines[i][MAX_LABEL - 1] = '\0';
        }
    }

    if (input->description != NULL) {
        output.notes = strdup(input->description);
    }

    return output;
}

void free_output_record(OutputRecord *output)
{
    if (output == NULL) {
        return;
    }

    free(output->notes);
    output->notes = NULL;

    for (int i = 0; i < output->ranked_ptr_count; ++i) {
        free(output->ranked_ptrs[i]);
        output->ranked_ptrs[i] = NULL;
    }
    output->ranked_ptr_count = 0;
}
