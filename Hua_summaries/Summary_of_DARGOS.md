#DARGOS

This paper is to introduce DARGOS which is a cloud monitoring solution that is decided under some directions of cloud towards to low overhead, scalability, high availability, self-discovery, dynamicity. Although there are a lot of notable monitoring applications today, none of them are designed under all considerations. The authors claim that DARGOS is the one that satisfies all requirements and applicable to modern cloud environments. The first reason why DARGOS is better than others is it is designed as DDS architecture, which grants high reliability and robustness, light-weight, flexibility, etc. DARGOS defines two entities, NMA and NSA, which are talking to each other and support unicast and multicast topology. The authors also design API and a console for users which enables the user can easily access the monitoring result. 

In the next, there is a section about the Openstack-based implementation of DARGOS. A NMA is attached to every compute service which collects data from sensors, which is the entity they define to identify resources, in physical node and hypervisor. In addition, it also has sensors to identify services, for instance the Apache HTTP and MySQL database. In this way, DARGOS can monitor the usage of both system resources and crucial services.

Then the the paper gives an evaluation on DARGOS:
<ol>
  <li>Network usage impact: DARGOS performs better than Openstack reference implementation for both periodic and event-based notifications.</li>
  <li>Comparison of Nagios, Lattice, DARGOS: DARGOS outperforms Lattice and Nagios in both unicast and multicast scenarios.</li>
  <li>DARGOS and Lattice scalability: DARGOS outperforms Lattice because of the lower size of DAGOS message.</li>
</ol>

Finally, the papers gives a real use case of DARGOS in cloud. The authors compare the node CPU usage of the nodes which use two different consolidation stratigies or not use any. And that proves cloud administrator or tenants can make decisions and trigger prompt control actions for different specific cloud requirements, by employing data from DARGOS.
