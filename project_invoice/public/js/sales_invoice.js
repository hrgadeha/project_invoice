frappe.ui.form.on("Project Table", {
  "project_code": function(frm,cdt,cdn) {
      frm.clear_table("items");
      frm.clear_table("timesheets");
      $.each(frm.doc.project_table, function(idx, d){
	if(d.project_code){
    frappe.call({
    "method": "project_invoice.project_invoice.invoice.getLabour",
args: {
project: d.project_code
},
callback:function(r){
	    for (var i=0;i<r.message.length;i++){
	    var row = frm.add_child("timesheets");
		    row.time_sheet = r.message[i][0];
		    row.billing_hours = r.message[i][1];
		    row.billing_amount = r.message[i][2];
	    }
        var row1 = frm.add_child("items");
        frappe.model.set_value(row1.doctype, row1.name, 'item_code',d.project_code);
        frappe.model.set_value(row1.doctype, row1.name, 'item_name',d.project_description);
        frappe.model.set_value(row1.doctype, row1.name, 'project',d.project_code);
        frappe.model.set_value(row1.doctype, row1.name, 'qty',1);
        frappe.model.set_value(row1.doctype, row1.name, 'labour',d.labour);
        frappe.model.set_value(row1.doctype, row1.name, 'washing',d.washing);
        frappe.model.set_value(row1.doctype, row1.name, 'materiel',d.material);
	}
    });
	}
  });
  },
  "washing": function(frm,cdt,cdn) {
      var d = locals[cdt][cdn];
      frappe.model.set_value(d.doctype, d.name, "total_cost", (d.material + d.washing + d.labour));
  },
  "labour": function(frm,cdt,cdn) {
      var d = locals[cdt][cdn];
      frappe.model.set_value(d.doctype, d.name, "total_cost", (d.material + d.washing + d.labour));
  },
  "material": function(frm,cdt,cdn) {
      var d = locals[cdt][cdn];
      frappe.model.set_value(d.doctype, d.name, "total_cost", (d.material + d.washing + d.labour));
  }
});

frappe.ui.form.on("Project Table", {
  "project_table_remove": function(frm,cdt,cdn) {
	  frm.clear_table("items");
      	  frm.clear_table("timesheets");
      $.each(frm.doc.project_table, function(idx, d){
	if(d.project_code){
    frappe.call({
    "method": "project_invoice.project_invoice.invoice.getLabour",
args: {
project: d.project_code
},
callback:function(r){
	    for (var i=0;i<r.message.length;i++){
	    var row = frm.add_child("timesheets");
		    row.time_sheet = r.message[i][0];
		    row.billing_hours = r.message[i][1];
		    row.billing_amount = r.message[i][2];
	    }
        var row1 = frm.add_child("items");
        frappe.model.set_value(row1.doctype, row1.name, 'item_code',d.project_code);
        frappe.model.set_value(row1.doctype, row1.name, 'item_name',d.project_description);
        frappe.model.set_value(row1.doctype, row1.name, 'project',d.project_code);
        frappe.model.set_value(row1.doctype, row1.name, 'qty',1);
        frappe.model.set_value(row1.doctype, row1.name, 'labour',d.labour);
        frappe.model.set_value(row1.doctype, row1.name, 'washing',d.washing);
        frappe.model.set_value(row1.doctype, row1.name, 'materiel',d.material);
	}
    });
	}
  });
  }
});

frappe.ui.form.on("Sales Invoice", {
  "invoice_type": function(frm) {
      frm.clear_table("items");
      frm.clear_table("timesheets");
      frm.clear_table("project_table");
      frm.set_value("selling_price_list","");
      cur_frm.refresh_fields();
  },
  "before_save": function(frm) {
    var labour = 0;
    var material = 0;
    var washing = 0;
      $.each(frm.doc.project_table || [], function(i, d) {
            washing = washing + d.washing;
		    material = material + d.material;
		    labour = labour + d.labour;
      });
        frm.set_value("total_washing", washing);
        frm.set_value("total_labour", labour);
        frm.set_value("total_material", material);
  }
});


frappe.ui.form.on("Sales Invoice", "refresh", function(frm){
	cur_frm.fields_dict['items'].grid.get_field('item_code').get_query = function(doc) {
        return {
            filters: [[
                'Item', 'is_project', '=', 0
            	     ]]
           	};
    	};
});

cur_frm.set_query("project_code", "project_table", function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];
	return{
		filters: [
			['Project', 'customer', '=', doc.customer],
			['Project', 'status', '=', "Open"]
		]
	};
});

frappe.ui.form.on('Project Table', {
	project_table_remove(frm,cdt,cdn) {
	    var d = locals[cdt][cdn];
		var tbl = frm.doc.items || [];
        var i = tbl.length;
            console.log(i);
            cur_frm.get_field("items").grid.grid_rows[i].remove();
            cur_frm.refresh();
	}
});
