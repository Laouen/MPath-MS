function stop_simulation(simulation_id) {
	$("#stop-icon").html("more_horiz");
	window.alert("stop simulation:" + simulation_id)
	//$.get("/Sim_RT_Runner/stop_simulation/" + simulation_id + "/");
}