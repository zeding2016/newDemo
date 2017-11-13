# -*- coding:utf-8 -*-
__author__ = 'zeding'
__mtime__ = '2017/11/10'

import xlwt;

# styleBlueBkg = xlwt.easyxf('font: color-index red, bold on');
# styleBlueBkg = xlwt.easyxf('font: background-color-index red, bold on');
# styleBlueBkg = xlwt.easyxf('pattern: pattern solid, fore_colour red;');
# styleBlueBkg = xlwt.easyxf('pattern: pattern solid, fore_colour blue;');
# styleBlueBkg = xlwt.easyxf('pattern: pattern solid, fore_colour light_blue;');
# styleBlueBkg = xlwt.easyxf('pattern: pattern solid, fore_colour pale_blue;');
# styleBlueBkg = xlwt.easyxf('pattern: pattern solid, fore_colour dark_blue;');
# styleBlueBkg = xlwt.easyxf('pattern: pattern solid, fore_colour dark_blue_ega;');
# styleBlueBkg = xlwt.easyxf('pattern: pattern solid, fore_colour ice_blue;');
styleBlueBkg = xlwt.easyxf( 'pattern: pattern solid, fore_colour red; font: bold on;' ) # 80% like
# styleBlueBkg = xlwt.easyxf('pattern: pattern solid, fore_colour sky_blue;');


# blueBkgFontStyle = xlwt.XFStyle()
# blueBkgFontStyle.Pattern = blueBackgroundPattern;
# styleBlueBkg = blueBkgFontStyle;

styleBold = xlwt.easyxf( 'font: bold on' )

wb = xlwt.Workbook();
ws = wb.add_sheet( 'realPropertyInfo' )

ws.write( 0, 0, "Sequence", styleBlueBkg )
ws.write( 0, 1, "MapID", styleBlueBkg )
ws.write( 0, 2, "Owner1", styleBold )
ws.write( 0, 3, "Owner2", styleBold )

wb.save( '/Users/zeding/Desktop/NewDemo/data/test.xls')