#!/bin/bash

# Seqscore command
scores="seqscore score --labels BIO --repair-method conlleval --reference"
errors="seqscore score --labels BIO --repair-method conlleval --error-counts --reference"


# Evaluate for all document types!
domains=("" "sports" "economy" "world_events")
doc_formats=("" "text_article" "data_report" "hybrid")

for domain in "${domains[@]}"; do
    for doc_format in "${doc_formats[@]}"; do

        doc_type=()
        [[ -n $domain ]] && doc_type+=("$domain")
        [[ -n $doc_format ]] && doc_type+=("$doc_format")

        # Evaluate XLM-FLERT for both versions
        for version in 03 sharp; do
            full=("$version" "${doc_type[@]}")
            joined=$(IFS=_; echo "${full[*]}")

            log="evals/xlm_flert/${version}/${joined}.txt"
            params="test_sets/conll_${version}/conll_${joined}.txt outputs/xlm_flert_${version}/xlm_flert_${joined}.txt"

            $scores $params > $log
            echo "" >> $log
            $errors $params >> $log
        done

        # Evaluate LUKE for CoNLL#
        full=("sharp" "${doc_type[@]}")
        joined=$(IFS=_; echo "${full[*]}")

        log="evals/luke/sharp/${joined}.txt"
        params="test_sets/conll_sharp/conll_${joined}.txt outputs/luke_sharp/luke_${joined}.txt"

        $scores $params > $log
        echo "" >> $log
        $errors $params >> $log


        # Evaluate ASP for CoNLL#
        just_doc=("${doc_type[@]}")
        join_doc=$(IFS=_; echo "${just_doc[*]}")


        log="evals/asp/sharp/asp_${joined}.txt"
        params="test_sets/conll_sharp_asp_order/conll_sharp_asp_order_${join_doc}.txt outputs/asp_sharp/asp_${joined}.txt"

        $scores $params > $log
        echo "" >> $log
        $errors $params >> $log

    done
done