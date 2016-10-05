def GetDateTimeFormatted(datetime_value):
    date_format ="%Y-%m-%d %H:%M:%S"
    return datetime.datetime.strptime(datetime_value.split(".")[0], date_format)
    
def ddhhmmss(seconds):
    dhms = ''
    for scale in 86400, 3600, 60:
        result, seconds = divmod(seconds, scale)
        if dhms != '' or result > 0:
            if(scale == 86400):
                dhms += str(int(result)) + "d "
            elif(scale == 3600):
                dhms += '{0:01g}'.format(result) + "h"
            elif(scale == 60):
                dhms += str(int(result)) + "m "

    dhms += str(int(seconds)) + "s"
    return dhms