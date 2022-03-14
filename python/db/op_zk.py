# -*- coding: utf-8 -*-
from kazoo.client import KazooClient


class ZkOpt:
    def __init__(self, url):
        self.url = url

    def echo_children(self, node_path_) -> None:
        zk = KazooClient(hosts=self.url)
        zk.start()
        # 获取某个节点下所有子节点
        node = zk.get_children(node_path_)
        zk.stop()
        print("node:{} 下所有子节点-->{}".format(node_path_, node))

    def echo_node_value(self, node_path_) -> None:
        zk = KazooClient(hosts=self.url)
        zk.start()

        # 获取某个节点对应的值
        value = zk.get(node_path_)
        zk.stop()
        print("node_path:{} 对应的值-->${}".format(node_path_, value))
        print(value)


if __name__ == '__main__':
    zk_host = "192.168.189.215:12181"
    node_path = "/Mgr/10031/Cluster"

    # 查询指定node对应的值value
    ZkOpt(zk_host).echo_node_value(node_path)

    # 查询指定node的所有子节点
    #ZkOpt(zk_host).echo_children(node_path)
