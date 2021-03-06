from odoo import fields, models
from datetime import datetime, timedelta

 
class ProductHistory(models.Model):
    """ Product history"""
    
    _name ='product.history'
    _description ='Maintain Product history'
    
    
    product_id = fields.Many2one('product.product', string='Product id', ondelete='cascade')
    product_tmpl_id = fields.Many2one('product.template', string='Product template id', ondelete='cascade')
    date = fields.Datetime(string='In Date')
    out_date = fields.Datetime(string='Out Date')
    order_id = fields.Many2one('pos.order', string='Product id', ondelete='cascade')
    status = fields.Char(string='status')
    created_by = fields.Many2one('res.users', string='Created user', ondelete='cascade')
    state = fields.Selection(
        [('draft', 'New'),('reserved', 'Reserved'),('noshow', 'No show'),
         ('checkin', 'CheckIn'),('checkout', 'CheckOut'),('cancel', 'Cancelled'),
         ('paid', 'Paid'), ('done', 'Posted'), ('invoiced', 'Invoiced'), 
         ('shift', 'Shifted'), ('extend', 'Extended'), ('block', 'Blocked'),],
        'Status',  copy=False, default='draft')
    block_room_id = fields.Many2one('hm.block.room', string='Block Room', ondelete='cascade')

 
class Producttemplate(models.Model): 
    _inherit='product.template'
    
    product_history_line_ids = fields.One2many('product.history', 'product_tmpl_id', string='Product template history')
    room_status = fields.Char(string='status')
    
 
class RoomStatus(models.Model):
    """Room Status"""
  
    _inherit = 'product.template'
    _description = "Status of the Rooms"
 
     
    def get_roomstatus(self, from_date, to_date):
 
        N = 2
        today = datetime.today()
        date_array=[]  
        ls=[]  
        date_format={}
        if(from_date and to_date):
            from_date = datetime.strptime(from_date, '%m/%d/%Y')
            to_date = datetime.strptime(to_date, '%m/%d/%Y')
            d1 = from_date.date()  # start date
            d2 = to_date.date()  # end date
            delta = d2 - d1         # timedelta
            N = delta.days + 1
            
        product_temp_ids = self.env['product.category'].search([ ('is_room', '=', True)])
        product_temp = self.env['product.template'].search([('categ_id', 'in', product_temp_ids.ids),
                                                               ('available_in_pos', '=', 'true')])
        list_product_arrays = {}
        list_order_arrays = {}
        categ_name = {}
        room_status_list_arrays = {} 
        if product_temp:  
            for products in product_temp:
                product_id_val = products.id
                key = ''
                protemp_id = self.env['product.history'].sudo().search([('product_tmpl_id', 'in', products.ids)])
                if protemp_id:
                    #product_history_ids_list = self.env['product.history'].sudo().search([])
                    if protemp_id:
                        for history in protemp_id:
                            product = history.product_id.id
                            if product != False:
                                product_arr =  self.env['product.product'].sudo().search([('id','=',product)])
                                rowdate = ""+datetime.strftime(history.date, "%b %d %Y")
                                rowdate1 = ""+datetime.strftime(history.out_date, "%b %d %Y")
                                d1 = datetime.strptime(rowdate, "%b %d %Y")
                                d2 = datetime.strptime(rowdate1, "%b %d %Y")
                                if(history.block_room_id):
                                    days = (abs((d2 - d1).days) + 1)
                                else:
                                    days = (abs((d2 - d1).days))

                                for i in range(days):
                                    if rowdate and rowdate1:
                                        range_dates = history.date + timedelta(i)
                                        d2 = datetime.strftime(range_dates, "%b %d %Y")
                                        key = str(product_id_val)+"-"+d2
                                        room_status_list_arrays[key] = history.state
                                        list_product_arrays[product_id_val] = products.name
                                        list_order_arrays[key] = history.order_id.id
                                        categ_name[product_id_val] = products.categ_id.name
                else:
                    list_product_arrays[product_id_val] = products.name
                    categ_name[product_id_val] = products.categ_id.name
                    
                    
        for i in range(N):
            if from_date and to_date:
                range_date = from_date + timedelta(i)
            else:
                range_date = datetime.now() - timedelta(i)
            date = datetime.strftime(range_date, "%b %d %Y") 
            date_1 = datetime.strptime(date, '%b %d %Y')
            date_value = datetime.strftime(range_date, "%a %m-%d-%Y")   
            today_date_value = datetime.strftime(today, "%b %d %Y")
            date_2 = datetime.strptime(today_date_value, '%b %d %Y')
            date_array.append(date)
            dates = date_array
            dates.sort(key=lambda date: datetime.strptime(date, "%b %d %Y"))
            date_format[date] = date_value  
            
            if(date_1 < date_2):
                date_date = datetime.strftime(date_1, "%b %d %Y")   
                ls.append(date_date)


        return {'date_key':dates, 'date_format':date_format, 'room_status_list_array':room_status_list_arrays,
                'list_product_array':list_product_arrays,'list_order_array':list_order_arrays,'categ_name':categ_name,
                'lesser_date':ls,}
