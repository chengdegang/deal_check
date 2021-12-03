import datetime
import os
import pdb
import paramiko

class SSH():
    """
    报错暂不可用
    """
    def __init__(self,host='10.244.10.13',user='root',pas='123',port=22):
        self.username = user,
        self.hostname = host,
        self.password = pas,
        self.port = port,
        self.ssh = paramiko.SSHClient()

    def connect(self):
        self.policy = paramiko.AutoAddPolicy()
        self.ssh.set_missing_host_key_policy(self.policy)
        try:
            self.ssh.connect(
                hostname=self.hostname,
                port=self.port,
                username=self.username,
                password=self.password
            )
        except Exception as e:
            print(f'connect failed: {e}')

    def run_cmd(self,cmd):
        try:
            stdin, stdout, stderr = self.ssh.exec_command(cmd, get_pty=True)
            res = stdout.read().decode('utf-8')
            err = stderr.read().decode('utf-8')
            result = res if res else err
            print(result)
        except Exception as e:
            print(f'command unusual: {e}')

    def close(self):
        print('close connect...')
        self.ssh.close()

def sshconnect(host='10.244.10.13',user='root',pas='123',por=22,cmd=''):
    """
    ssh连接服务器并可以处理多条shell命令，用;分割
    """
    # pdb.set_trace()
    ssh = paramiko.SSHClient()
    policy = paramiko.AutoAddPolicy()
    ssh.set_missing_host_key_policy(policy)
    ssh.connect(
        hostname=host,
        port=por,
        username=user,
        password=pas
    )
    try:
        stdin, stdout, stderr = ssh.exec_command(cmd,get_pty=True)
        res = stdout.read().decode('utf-8')
        err = stderr.read().decode('utf-8')
        result = res if res else err
        print(result)
    except Exception as e:
        print(e)
    finally:
        ssh.close()

def up(local_file, remote_path):
    hostname = '10.244.10.13',
    port = 22,
    username = 'root',
    password = '123'
    try:
        t = paramiko.Transport((hostname, port))
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        print('开始上传文件%s ' % datetime.datetime.now())

        try:
            sftp.put(local_file, remote_path)
        except Exception as e:
            sftp.mkdir(os.path.split(remote_path)[0])
            sftp.put(local_file, remote_path)
            print("从本地： %s 上传到： %s" % (local_file, remote_path))
        print('文件上传成功 %s ' % datetime.datetime.now())
        t.close()
    except Exception as e:
        print(repr(e))

if __name__ == '__main__':
    # up('/Users/jackrechard/Desktop/tp.png','/home/chengdegang/put')
    # newcon = SSH()
    # newcon.connect()
    # newcon.run_cmd('ls')

    sshconnect(host='10.244.10.13',pas='123',user='root',cmd='cd /home/chengdegang/put;pwd')
