#!/usr/bin/python

import collectd
from ouimeaux.environment import Environment, UnknownDevice

CONFIG=[]
ENV = Environment(with_cache=False)

def init():
    collectd.info("start")
    ENV.start()
    #collectd.info("Discover")
    ENV.discover()

def read():
    #collectd.info("read")
    
    for name in CONFIG:
        
      while True:
        #collectd.info("querying: " + name)
        try:
            switch = ENV.get_switch(name)

            v1 = collectd.Values(plugin='wemo')
            v1.type = 'power'
            v1.type_instance = 'power'
            v1.plugin_instance = name

            power = switch.current_power/1000.0

            collectd.info("Got power from %s = %fW" % (name, power))

            v1.values = [power]
            v1.dispatch()
        except UnknownDevice:
            collectd.error("Unknown device: " + name)
        except ConnectionError:
            ENV.start()
            ENV.discover()
            continue

        break

    env = None

def config_callback(conf):
    name = None

    for node in conf.children:
        key = node.key.lower()
        val = node.values[0]


        if key == 'name':
            #collectd.info("found config name = " + val)
            CONFIG.append(val)
        else:
            collectd.warning('unknown config key: %s' % key)
            continue

collectd.register_config(config_callback)
collectd.register_init(init)
collectd.register_read(read)
