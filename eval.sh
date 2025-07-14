#!/bin/bash

# Seqscore command
seq="seqscore score --labels BIO --repair-method conlleval --reference"

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

            cmd="$seq test_sets/conll_${version}/conll_${joined}.txt outputs/xlm_flert_${version}/xlm_flert_${joined}.txt"
            log="evals/xlm_flert/${version}/${joined}.txt"

            $cmd > $log
        done

        # Evaluate LUKE for CoNLL#
        full=("sharp" "${doc_type[@]}")
        joined=$(IFS=_; echo "${full[*]}")

        cmd = "$seq test_sets/conll_sharp/conll_sharp_${joined}.txt outputs/luke_sharp/luke_sharp_${joined}.txt"
        log="evals/luke/sharp/${joined}.txt"
        $cmd > $log


        # Evaluate ASP for CoNLL#
        cmd = "$seq test_sets/conll_sharp_asp_order/conll_sharp_asp_order${joined}.txt outputs/asp_sharp/asp_sharp_${joined}.txt"
        log="evals/asp/sharp/${joined}.txt"
        $cmd > $log

    done
done