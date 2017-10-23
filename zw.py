# coding:utf-8
# from xml.etree.ElementTree import ElementTree,Element
import xml.etree.ElementTree as ET
import types


def read_xml(in_path):
    '''读取并解析xml文件
       in_path: xml路径
       return： ElementTree'''
    tree = ET.ElementTree()
    tree.parse(in_path)
    return tree


def write_xml(tree, out_path):
    '''将XML文件写出
        tree: xml 树
        out_path： 输出路径'''
    tree.write(out_path, encoding="utf-8", xml_declaration=True)


def DBpool(count):
    '''将分库配置文件输出'''
    for pool in root.iter('pool-params'):
        i = 1
        while i < count:
            authorE = ET.Element('pool-param')
            authorE.set('id', '%s' % i)
            b = ET.SubElement(authorE, 'property', attrib={"name": "url"})
            b.text = 'jdbc:oracle:thin:@10.128.136.162:1521:dakdb'
            c = ET.SubElement(authorE, 'property', attrib={"name": "username"})
            c.text = 'co_ntr_st_dcacct0'
            d = ET.SubElement(authorE, 'property', attrib={"name": "password"})
            d.text = 'co_ntr_st_dcacct0'
            e = ET.SubElement(authorE, 'property', attrib={"name": "driverClassName"})
            e.text = 'oracle.jdbc.driver.OracleDriver'
            f = ET.SubElement(authorE, 'property', attrib={"name": "initialSize"})
            f.text = '10'
            g = ET.SubElement(authorE, 'property', attrib={"name": "maxActive"})
            g.text = '50'
            h = ET.SubElement(authorE, 'property', attrib={"name": "minIdle"})
            h.text = '10'
            n = ET.SubElement(authorE, 'property', attrib={"name": "maxWait"})
            n.text = '20000'
            j = ET.SubElement(authorE, 'property', attrib={"name": "removeAbandoned"})
            j.text = 'true'
            k = ET.SubElement(authorE, 'property', attrib={"name": "removeAbandonedTimeout"})
            k.text = '600'
            l = ET.SubElement(authorE, 'property', attrib={"name": "timeBetweenEvictionRunsMillis"})
            l.text = '600'
            m = ET.SubElement(authorE, 'property', attrib={"name": "minEvictableIdleTimeMillis"})
            m.text = '120000'
            o = ET.SubElement(authorE, 'property', attrib={"name": "validationQuery"})
            o.text = '120000'
            p = ET.SubElement(authorE, 'property', attrib={"name": "validationInterval"})
            p.text = '30000'
            q = ET.SubElement(authorE, 'property', attrib={"name": "testWhileIdle"})
            q.text = 'true'
            r = ET.SubElement(authorE, 'property', attrib={"name": "testOnBorrow"})
            r.text = 'false'
            s = ET.SubElement(authorE, 'property', attrib={"name": "testOnReturn"})
            s.text = 'false'
            pool.append(authorE)
            i += 1


def DBTBpool():
    for fun in root.iter('property'):
        if fun.get('name') == 'dbCount':
            fun.text = '%s' % dbcount
        if fun.get('name') == 'tbCount':
            fun.text = '%s' % tbcount


if __name__ == "__main__":
    tree = read_xml("1.xml")
    dbcount = int(raw_input("几个分库> ".decode('utf-8').encode('gbk')))
    tbcount = int(raw_input("几个分表> ".decode('utf-8').encode('gbk')))
    root = tree.getroot()
    #  判断是否分库
    #  不分库分表
    if dbcount == 1:
        #  修改base_SingleNode 值
        for base_single in tree.iterfind('system/property[@name="base_SingleNode"]'):
            base_single.set('value', 'true')
        # 修改<tables>
        for child in root.iterfind('tables/table'):
            if tbcount == 1:
                child.set('shardingTable', 'false')
            else:
                child.set('shardingTable', 'true')
            child.set('dataNodeRef', "dn0")
        # 修改<dataNodes>
        for data in root.iterfind('dataNodes/dataNode'):
            data.set('name', 'dn0')
            #  修改<datasource>
        for datasource in root.iterfind('dataSources/dataSource'):
            datasource.set('name', 'dn0-0')
            #  修改<pool-param>
        for pool in root.iterfind('dataSources/dataSource/pool-params/pool-param'):
            pool.set('id', '0')
        # 修改<functions>
        DBTBpool()
        #   分库分表
    elif dbcount > 1:
        for base_single in tree.iterfind('system/property[@name="base_SingleNode"]'):
            base_single.set('value', 'false')
        # 修改<tables>
        for child in root.iterfind('tables/table'):
            if tbcount == 1:
                child.set('shardingTable', 'false')
            else:
                child.set('shardingTable', 'true')
            child.set('dataNodeRef', "dn$0-%s" % (dbcount - 1))
        # 修改<dataNodes>
        for data in root.iterfind('dataNodes/dataNode'):
            data.set('name', 'dn$0-%s' % (dbcount - 1))
            #  修改<datasource>
        for datasource in root.iterfind('dataSources/dataSource'):
            datasource.set('name', 'dn$(0-%s)-0' % (dbcount - 1))
            #  修改<pool-param>
        DBpool(dbcount)
        #  修改<functions>
        DBTBpool()


    else:
        exit(0)

    # 写入XML
    write_xml(tree, '50.xml')


