This paper is to introduce DARGOS which is a cloud monitoring solution that is decided under some directions of cloud towards to low overhead, scalability, high availability, self-discovery, dynamicity. Although there are a lot of notable monitoring applications today, none of them are designed under all considerations. The authors claim that DARGOS is the one that satisfies all requirements and applicable to modern cloud environments. The first reason why DARGOS is better than others is it is designed as DDS architecture, which grants high reliability and robustness, light-weight, flexibility, etc. DARGOS defines two entities, NMA and NSA, which are talking to each other and support unicast and multicast topology. The authors also design API and a console for users which enables the user can easily access the monitoring result.

Then the the paper gives an evaluation on DARGOS:

Network usage impact: DARGOS performs better than Openstack reference implementation for both periodic and event-based notifications.

Comparison of Nagios, Lattice, DARGOS: DARGOS outperforms Lattice and Nagios in both unicast and multicast scenarios.

DARGOS and Lattice scalability: DARGOS outperforms Lattice because of the lower size of DAGOS message.
