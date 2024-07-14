from openerp import models, fields, api
import re, datetime
import requests

def send_telegram(message, user_id):
  token = "7263009682:AAGHf5d4k484T_5da4b9yLa9JDvUSd8Sl2o"
  chat_id = "-1002196534446"
  # Dani
  if user_id == 11:
    token = "7090690825:AAGDtcVTUNPfgsLkrRItjocj8uDuHbE4Szs"
    chat_id = "-1002232803613"
  # Agus
  elif user_id == 9:
    token = "7212599223:AAEe2acDQYFq7Wy0X64eSptbXfsh1Co21Ek"
    chat_id = "-1002186361212"
  # Top Office
  elif user_id == 12:
    token = "7257697185:AAEIJcwtXcRq-3vsTYWbpFDiuwAgEPN7PDc"
    chat_id = "-1002247585047"
  # Zul
  elif user_id == 5:
    token = "7491181830:AAGM7iZVtxqJH624Zno2oaCrqGMTv81jbzY"
    chat_id = "-1002166849753"
  # Dev
  else:
    token = "7263009682:AAGHf5d4k484T_5da4b9yLa9JDvUSd8Sl2o"
    chat_id = "-1002196534446"
    message = message + "%0AUser ID : " + str(user_id)
  url = "https://api.telegram.org/bot"+token+"/sendMessage?chat_id="+chat_id+"&text="+message
  response = requests.get(url).json()

def sep(s, thou=".", dec=","):
  integer, decimal = s.split(".")
  integer = re.sub(r"\B(?=(?:\d{3})+$)", thou, integer)
  return integer + dec + decimal

class sale_order(models.Model):
  _inherit = 'sale.order'

  @api.multi
  def write(self, vals):
    try:
      uid = self.env.uid
      if self.type == "sale_order":
        origin_old=self.origin
        toko = self.partner_id.name
        message = ""
        lines_new = vals.get('order_line')
        state_old = self.state
        state_new = vals.get('state')
        
        # Cek Jika ada perubahan status s.o
        if state_new:
          if state_new != state_old:
            message = message + state_old + " %E2%9E%A1%EF%B8%8F " + state_new + "%0A%0A"

        # Cek Jika ada perubahan baris s.o
        if lines_new:
          for line in lines_new:
            operation_flag=line[0]
            # Jika dihapus
            if operation_flag == 2:
              soline_old = self.env['sale.order.line'].search([('id', '=', line[1])])
              if soline_old:
                message = message + "%E2%9D%8C" + soline_old.product_id.name + "%0A%0A"
            # Cek Jika Tipe Data Dictionary
            if isinstance(line[2], dict):
              product_id_val = line[2].get('product_id')
              product_new = line[2].get('name')
              quantity=line[2].get('quantity')
              uos_id_val = line[2].get('product_uom')
              harga=line[2].get('price_unit')
              soline_old = self.env['sale.order.line'].search([('id', '=', line[1])])
              # Jika Edit baris
              if soline_old:
                product_old = soline_old.product_id.name
                # Perubahan Kuantitas
                if quantity:
                  uos_old = soline_old.uos_id.name
                  uos_new = uos_old
                  if uos_id_val:
                    product_uom = self.env['product.uom'].search([('id', '=', uos_id_val)])
                    uos_new = product_uom.name
                  qty_old = sep('%.1f'%(soline_old.quantity)) + " " + uos_old
                  qty_new = sep('%.1f'%(quantity)) + " " + uos_new
                  if qty_old != qty_new:
                    message=message + product_old + "%0A Qty " +  qty_old + " %E2%9E%A1%EF%B8%8F " + qty_new + "%0A%0A"
                # Perubahan Harga
                if harga:
                  harga_old = sep('%.1f'%(soline_old.price_unit))
                  harga_new = sep('%.1f'%(harga))
                  if harga_old != harga_new:
                    message=message + product_old + "%0A Harga " + harga_old + " %E2%9E%A1%EF%B8%8F " + harga_new + "%0A%0A"
                # Perubahan Product
                if product_id_val:
                  if product_id_val != soline_old.product_id:
                    message = message + product_old + "%0A %E2%AC%87%EF%B8%8F %0A" + product_new + "%0A%0A"
              # Jika Baris Baru
              else:
                product_new = line[2].get('name')
                message=message + "%E2%9E%95" + product_new + "%0A%0A"
        if message != "":
          send_telegram(origin_old + " " + toko + "%0A%0A" + message,uid)
    except Exception as e:
      # If any other exception occurs, execute this code
      send_telegram(str(e), 1)
    finally:
      # This code will always execute, regardless of whether an exception occurs or not
      return super(sale_order, self).write(vals)
      
class account_invoice(models.Model):
  _inherit = 'account.invoice'
  
  @api.multi
  def write(self, vals):
    try:
      uid = self.env.uid
      if self.type == "out_invoice":
        origin_old=self.origin
        toko = self.partner_id.name
        message = ""
        lines_new = vals.get('invoice_line')
        state_old = self.state
        state_new = vals.get('state')
        
        # Cek Jika ada perubahan status faktur
        if state_new:
          if state_new != state_old:
            message = message + state_old + " %E2%9E%A1%EF%B8%8F " + state_new + "%0A%0A"

        # Cek Jika ada perubahan baris faktur
        if lines_new:
          for line in lines_new:
            operation_flag=line[0]
            # Jika dihapus
            if operation_flag == 2:
              invline_old = self.env['account.invoice.line'].search([('id', '=', line[1])])
              if invline_old:
                message = message + "%E2%9D%8C" + invline_old.product_id.name + "%0A%0A"
            # Cek Jika Tipe Data Dictionary
            if isinstance(line[2], dict):
              product_id_val = line[2].get('product_id')
              product_new = line[2].get('name')
              quantity=line[2].get('quantity')
              uos_id_val = line[2].get('uos_id')
              harga=line[2].get('price_unit')
              invline_old = self.env['account.invoice.line'].search([('id', '=', line[1])])
              # Jika Edit baris
              if invline_old:
                product_old = invline_old.product_id.name
                # Perubahan Kuantitas
                if quantity:
                  uos_old = invline_old.uos_id.name
                  uos_new = uos_old
                  if uos_id_val:
                    product_uom = self.env['product.uom'].search([('id', '=', uos_id_val)])
                    uos_new = product_uom.name
                  qty_old = sep('%.1f'%(invline_old.quantity)) + " " + uos_old
                  qty_new = sep('%.1f'%(quantity)) + " " + uos_new
                  if qty_old != qty_new:
                    message=message + product_old + "%0A Qty " +  qty_old + " %E2%9E%A1%EF%B8%8F " + qty_new + "%0A%0A"
                # Perubahan Harga
                if harga:
                  harga_old = sep('%.1f'%(invline_old.price_unit))
                  harga_new = sep('%.1f'%(harga))
                  if harga_old != harga_new:
                    message=message + product_old + "%0A Harga " + harga_old + " %E2%9E%A1%EF%B8%8F " + harga_new + "%0A%0A"
                # Perubahan Product
                if product_id_val:
                  if product_id_val != invline_old.product_id:
                    message = message + product_old + "%0A %E2%AC%87%EF%B8%8F %0A" + product_new + "%0A%0A"
              # Jika Baris Baru
              else:
                product_new = line[2].get('name')
                message=message + "%E2%9E%95" + product_new + "%0A%0A"
        if message != "":
          send_telegram(origin_old + " " + toko + "%0A%0A" + message,uid)
    except Exception as e:
      # If any other exception occurs, execute this code
      send_telegram(str(e), 1)
    finally:
      # This code will always execute, regardless of whether an exception occurs or not
      return super(account_invoice, self).write(vals)
