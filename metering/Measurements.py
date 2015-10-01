
def compute():
	dict = {
		'instance':'Gauge',
		'memory':'Gauge',
		'memory_usage':'Gauge',
		'cpu':'Cumulative',
		'cpu_util':'Gauge',
		'vcpus':'Gauge',
		'disk.read.requests':'Cumulative',
		'disk.read.requests.rate':'Gauge',
		'disk.write.requests':'Cumulative',
		'disk.write.requests.rate':'Gauge',
		'disk.read.bytes':'Cumulative',
		'disk.read.bytes.rate':'Gauge',
		'disk.write.bytes':'Cumulative',
		'disk.write.bytes.rate':'Gauge',
		'disk.root.size':'Gauge',
		'disk.ephemeral.size':'Gauge',
		'network.incoming.bytes':'Cumulative',
		'network.incoming.bytes.rate':'Gauge',
		'network.outgoing.bytes':'Cumulative',
		'network.outgoing.bytes.rate':'Gauge',
		'network.incoming.packets':'Cumulative',
		'network.incoming.packets.rate':'Gauge',
		'network.outgoing.packets':'Cumulative',
		'network.outgoing.packets.rate':'Gauge'}
	return dict

