<?php

/**
 * @file
 * Provides views runtime hooks for views.module.
 */

use Drupal\views\ViewExecutable;
use Drupal\views\Plugin\views\PluginBase;


function views_views_query_alter(ViewExecutable $view, QueryPluginBase $query){
  echo("HAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA ALTER");
  print dpm($view->name);
  drupal_set_message($view->name);
  //if ($view->name == "view_coursework_submitted") {
     //$join = new views_join;
     //$join->construct('TABLE NAME', 'NODE', 'nid', 'entity_id', '', 'LEFT');

     //$view->query->add_relationship('TABLE NAME', $join, 'node');
     $query->add_where('field_coursework_file_file_managed__node__field_teachers_with_access_to_th', 'field_coursework_file_file_managed__node__field_teachers_with_access_to_th.field_teachers_with_access_to_th_value', '%' + $account->getUsername() + '%', 'LIKE');
  //}
}


/**
 * Implements hook_views_query_substitutions().
 *
 * Makes the following substitutions:
 * - Current time.
 * - Drupal version.
 * - Special language codes; see
 *   \Drupal\views\Plugin\views\PluginBase::listLanguages().
 */
function views_views_query_substitutions(ViewExecutable $view) {
  $substitutions = array(
    '***CURRENT_VERSION***' => \Drupal::VERSION,
    '***CURRENT_TIME***' => REQUEST_TIME,
  ) + PluginBase::queryLanguageSubstitutions();

  return $substitutions;
}
