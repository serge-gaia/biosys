var biosys = biosys || {};

biosys.view_data = function ($, _, moduleOptions) {
    "use strict";
    var options = moduleOptions,
        defaultTableOptions = {
            paging: true,
            info: true,
            searching: true,
            scrollCollapse: true,
            processing: true,
            deferRender: true,
            serverSide: false,
            autowidth: false,
            scrollX: true
        },
        selectors = options.selectors,
        data = options.data,
        $tablePanel = $(selectors.tablePanel),
        $tabletitle = $(selectors.tableTitle),
        dataTable,
        datasets;

    function initProjectFilter() {
        var $select = $(selectors.projectFilter);
        $select.select2({
            placeholder: 'Select project',
            allowClear: true
        });
        $select.on('change', function (e) {
            var url = '/api/v2/dataset/?project__id=' + $(e.target).val();
            $.ajax(url, {
                    data: 'json'
                }
            ).then(function (data) {
                showDatasets(data.objects || []);
            });
        });
    }

    function showDatasets(dss) {
        var nodeTemplate = _.template(
            '<li role="presentation" id="id-nav-<%= name %>" data-view="<%= name %>" class=""><a href="#"><%= name %></a></li>'
            ),
            $navPanel = $(selectors.navPanel),
            $node;
        datasets = dss;
        $navPanel.children().remove();
        clearDataPanel();
        _.forEach(datasets, function (ds) {
            $node = $(nodeTemplate({name: ds.name}));
            $node.on('click', function (e) {
                showData($(e.target).parent().attr('data-view'));
            });
            $navPanel.append($node);
        });
    }

    function clearDataPanel(){
        $tablePanel.children().remove();
        $tabletitle.text('');
    }

    function showData(name) {
        var ds = _.filter(datasets, function (ds) {
            return ds.name === name;
        }),
            headers,
            colDefs,
            $tableNode,
            url,
            tableOptions;
        clearDataPanel();
        $tableNode = $('<table id="data-table" class="table table-bordered table-responsive"></table>');
        $tablePanel.append($tableNode);
        if (ds.length > 0) {
            ds = ds[0];
            headers = _.map(ds.data_package.resources[0].schema.fields, function (field) {
                return field.name;
            });
            colDefs = _.map(headers, function (header) {
                return {
                    'title': header,
                    'name': header,
                    'data': header
                };
            });
            url = '/publish/data/' + ds.id;
            tableOptions = $.extend({}, defaultTableOptions, {
                    ajax: {
                        url: url,
                        method: 'get',
                        error: function (xhr, textStatus, thrownError) {
                            console.log("Error while loading applications data:", thrownError, textStatus, xhr.responseText, xhr.status);
                            //Stop the data table 'Processing'.
                            //$(options.selectors.applicationsTable + '_processing').hide();
                        }
                    }
                });
            dataTable = biosys.dataTable.initTable($tableNode, tableOptions,  colDefs);
            $tabletitle.text(name);
        }
    }

    return {
        init: function () {
            initProjectFilter();
            //$('select').select2();
        }
    };
};
