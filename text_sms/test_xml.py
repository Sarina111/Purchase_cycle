import psycopg2

CONNECT_ARGS = 'host=localhost user=jenish password=jjenishh dbname=newdb'


def exportPlants(outfileName):
    outfile = file(outfileName, 'w')  #opens file for writing
    connection = psycopg2.connect(CONNECT_ARGS)
    cursor = connection.cursor()
    cursor.execute("select * from hr.emplooyee")
    rows = cursor.fetchall()
    outfile.write('<?xml version="1.0" ?>\n')
    outfile.write('<mydata>\n')
    for row in rows:
        outfile.write('  <row>\n')
        outfile.write('    <name>%s</name>\n' % row[0])
        outfile.write('    <desc>%s</desc>\n' % row[1])
        outfile.write('    <rating>%s</rating>\n' % row[2])
        outfile.write('    <rating>%s</rating>\n' % row[3])
        outfile.write('    <rating>%s</rating>\n' % row[4])
        outfile.write('    <rating>%s</rating>\n' % row[5])
        outfile.write('    <rating>%s</rating>\n' % row[6])
        outfile.write('    <rating>%s</rating>\n' % row[7])
        outfile.write('  </row>\n')
    outfile.write('</mydata>\n')
    outfile.close()




# exportPlants('out6')
