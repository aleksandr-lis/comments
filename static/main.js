'use strict'

var sid = 'some_session_id'

window.onload = function() {

  // First level only

  loadComments(
    { 'article_id': '1' },
    'for-article1'
  )

  // Full threads

  loadComments(
    { 'article_id': '1', 'threads': 'yes' },
    'for-article2'
  )

  // Single comment with thread

  loadComments(
    { 'comment_id': '1', 'threads': 'yes' },
    'for-comment'
  )

  // By person

  loadComments(
    { 'person_id': '1' },
    'for-person'
  )

  // Log

  loadLog(
    { 'comment_id': '8' },
    'for-log'
  )

  // end onLoad

}

function loadComments(params, target) {
  $.post(
    '/comment/list/',
    params,
    function(data) {
      for (var d in data) {
        $('div#' + target).append(row2html(data[d]))
      }
    }, 'json'
  )
}

function row2html(item) {
  var elem = $('<div class="uk-container uk-container-small"/>')
  elem.attr('id', item.id)
  elem.append($('<p/>').text(item.content))
  if (item.person) {
    elem.append($('<span/>').text(item.person))
  }
  elem.append($('<span/>').text(item.created))

  var act = $($('<div class="actions"/>'))
  act.append($('<a class="comment-add" rel="comment"/>').text('Reply'))
  act.append($('<a class="comment-edit" rel="comment"/>').text('Edit'))
  act.append($('<a class="comment-delete" rel="comment"/>').text('Delete'))

  elem.append(act)

  if (item.childs.length) {
    var elem_c = $('<div/>')
    elem_c.addClass('childs')
    for (var c in item.childs) {
      elem_c.append(row2html(item.childs[c]))
    }
    elem.append(elem_c)
  }

  return elem
}

// Log

function loadLog(params, target) {
  $.post(
    '/comment/log/',
    params,
    function(data) {
      for (var d in data) {
        $('div#' + target).append(log2html(data[d]))
      }
    }, 'json'
  )
}

function log2html(item) {
  var elem = $('<div class="uk-container uk-container-small"/>')
  elem.append($('<p/>').text(item.before || '—'))
  elem.append($('<p/>').text(item.after || '—'))
  elem.append($('<br clear="all"/>'))
  if (item.type == 'i') {
    elem.append($('<span/>').text('Created by ' + item.person))
  } else if (item.type == 'u') {
    elem.append($('<span/>').text('Edited by ' + item.person))
  } else if (item.type == 'd') {
    elem.append($('<span/>').text('Deleted by ' + item.person))
  }
  elem.append($('<span/>').text(item.created))

  return elem
}

// Comment add link

$(document).on('click', 'a.comment-add', function(event){
  event.preventDefault()

  $('div#form-add').hide()
  $('div#form-edit').hide()

  $('div.actions').show()
  $(event.target).closest('div.actions').hide()

  if ($(event.target).attr('rel') == 'comment') {
    $('div#form-add input[name=article_id]').val('')
    $('div#form-add input[name=comment_id]').val(
      $(event.target).closest('div.uk-container').attr('id')
    )
  } else if ($(event.target).attr('rel') == 'article') {
    $('div#form-add input[name=article_id]').val(
      $(event.target).closest('div.uk-container').attr('id')
    )
    $('div#form-add input[name=comment_id]').val('')
  }

  $('div#form-add').insertAfter($(event.target).closest('div.actions'))
  $('div#form-add').show()
})

// Comment add action

$(document).on('click', 'div#form-add * button.uk-button-primary', function(event){
  event.preventDefault()

  var article_id = $('div#form-add * input[name=article_id]').val()
  var comment_id = $('div#form-add * input[name=comment_id]').val()
  var content = $('div#form-add * textarea').val()

  $.post(
    '/comment/add/',
    {
      'article_id': article_id,
      'comment_id': comment_id,
      'sid': sid,
      'content': content,
    },
    function(data) {
      if (data.error) {
        alert(data.error)
      } else {
        document.location.href = '/'
      }
    }, 'json'
  )
})

// Comment edit link

$(document).on('click', 'a.comment-edit', function(event){
  event.preventDefault()

  $('div#form-add').hide()
  $('div#form-edit').hide()

  $('div.actions').show()
  $(event.target).closest('div.actions').hide()

  $('div#form-edit input[name=comment_id]').val(
    $(event.target).closest('div.uk-container').attr('id')
  )
  // console.log($(event.target).closest('div.uk-container p').eq(0).text())
  $('div#form-edit textarea').val(
    $(event.target).closest('div.uk-container').find('p').first().text()
  )

  $('div#form-edit').insertAfter($(event.target).closest('div.actions'))
  $('div#form-edit').show()
})

// Comment edit action

$(document).on('click', 'div#form-edit * button.uk-button-primary', function(event){
  event.preventDefault()

  var comment_id = $('div#form-edit * input[name=comment_id]').val()
  var content = $('div#form-edit * textarea').val()

  $.post(
    '/comment/edit/',
    {
      'comment_id': comment_id,
      'sid': sid,
      'content': content,
    },
    function(data) {
      if (data.error) {
        alert(data.error)
      } else {
        document.location.href = '/'
      }
    }, 'json'
  )
})

// Comment delete

$(document).on('click', 'a.comment-delete', function(event){
  event.preventDefault()

  if (!confirm('Are you sure?')) {
    return false
  }

  var comment_id = $(event.target).closest('div.uk-container').attr('id')

  $.post(
    '/comment/delete/',
    {
      'comment_id': comment_id,
      'sid': sid,
    },
    function(data) {
      if (data.error) {
        alert(data.error)
      } else {
        document.location.href = '/'
      }
    }, 'json'
  )
})
