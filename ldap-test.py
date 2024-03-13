from ldap3 import Server, Connection, ANONYMOUS, ALL
import click
import threading

'''
ldap 未授权检查工具 by lbb
20240213
v1.0
'''

# 创建一个锁对象
output_lock = threading.Lock()


# 命令参数
@click.command()
@click.option('-l', '--lists', help='把资产文件放在和当前程序同级目录且文本格式为ip+端口号')
@click.option('-t', '--target', help='单个地址')
def run(lists, target):
    brander()
    if lists is None and target is None:
        exit("未指定参数")

    if not (target is None):
        check_unauthorized_ldap(target)

    if not (lists is None):
        with open(lists, 'r', encoding='utf-8') as f:
            threads = []
            for i in f.readlines():
                target = i.strip("\n")
                thread = threading.Thread(target=check_unauthorized_ldap, args=(target,))
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()


def brander():
    branders = '''
    =========================
    = ldap 未授权检查       =
    =         by lbb v1.0   =
    =========================
    '''
    print(branders)


def check_unauthorized_ldap(target):
    try:
        # 创建 LDAP 服务器对象 并设置连接超时为3秒
        server = Server(target, get_info=ALL, connect_timeout=3)
        # 尝试匿名连接
        conn = Connection(server, authentication=ANONYMOUS)
        # 连接到 LDAP 服务器
        if conn.bind():
            with output_lock:
                click.secho(f"消息提示[+]{target}存在 LDAP 未授权访问！", fg='red')
        else:
            with output_lock:
                click.secho(f"消息提示[+]{target}LDAP 不存在未授权访问！", fg='green')
    except Exception:
        with output_lock:
            click.secho(f"消息提示[+] 建立连接失败！", fg='yellow')


if __name__ == "__main__":
    run()
