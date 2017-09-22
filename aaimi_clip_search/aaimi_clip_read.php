<?php 
# Run Python script to search link file and return results for search terms
$category = $_POST['folder'];
$terms = $_POST['keys'];
$aaimisearch = "python aaimi_clip_web_read.py " . $category . " " . $terms;
$search_results = system($aaimisearch);
$lines = preg_split('/\n/', $search_results, -1, PREG_SPLIT_NO_EMPTY);
?>
