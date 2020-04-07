#pragma once
// api.cpp : Defines the exported functions for the DLL.
//

#include "api.h"

using namespace std::literals::chrono_literals;

// This is the constructor of a class that has been exported.
Capi::Capi()
{
	createConsole();
	printf("console created\n");
	reward = 0.f;
	is_client_connected = false;
}

void Capi::init() {
	createServer();
}

//Capi::~Capi()
//{
//	closesocket(client_socket);
//	cout << "Client disconnected." << endl;
//}

void Capi::createConsole()
{
	AllocConsole();
	freopen_s((FILE**)stdout, "CONOUT$", "wb", stdout);
	freopen_s((FILE**)stderr, "CONOUT$", "wb", stderr);
	freopen_s((FILE**)stdin, "CONIN$", "rb", stdin);
	SetConsoleTitle(L"Debug");
}

void Capi::createServer() {

	WSADATA WSAData;

	SOCKADDR_IN serverAddr, clientAddr;

	WSAStartup(MAKEWORD(2, 0), &WSAData);
	server_socket = socket(AF_INET, SOCK_STREAM, 0);

	serverAddr.sin_addr.s_addr = INADDR_ANY;
	serverAddr.sin_family = AF_INET;
	serverAddr.sin_port = htons(3121);

	bind(server_socket, (SOCKADDR*)& serverAddr, sizeof(serverAddr));
	listen(server_socket, 0);

	cout << "Listening for incoming connections..." << endl;

	char buffer[1024];
	string message;
	int clientAddrSize = sizeof(clientAddr);
	if ((client_socket = accept(server_socket, (SOCKADDR*)& clientAddr, &clientAddrSize)) != INVALID_SOCKET)
	{
		u_long iMode = 1;
		ioctlsocket(client_socket, FIONBIO, &iMode);
		cout << "Client connected!" << endl;
		is_client_connected = true;
	}
}

void Capi::handleMessage(string message) {
	if (message.length() == 0) {
		cout << "Message is none" << endl;
	}

	else if (message == "close") {
		sendReward();
	}

	else if (message == "get_reward") {
		sendReward();
	}

	else if (message == "kill_bots") {
		// TODO send command "kill bots"
		cout << "Killing bots" << endl;
	}
	else {
		cout << "Unknown message : " << endl;
		cout << "\tLength =  " << message.length() << endl;
		cout << "\tpayload =  " << message << endl;
	}
}

SOCKET Capi::get_client_socket()
{
	return client_socket;
}

void Capi::computeReward(CUserCmd* pCmd) {
	
	p_cmd = pCmd;

	// Updating player info
	my_index = g_pEngine->GetLocalPlayer();
	p_local_player = g_pEntityList->GetClientEntity(my_index);
	my_team = p_local_player->GetTeam();

	my_view_angles = p_cmd->viewangles;
	vec_aim_direction = my_view_angles.toVector();
	point_my_position = p_local_player->GetEyePosition();

	// Computing reward value
	if (!computeIfHit()) // if an ennemy player is being aimed at
		computeClosest(); // if no ennemy player is being aimed at

	// cout << reward << endl;
}

bool Capi::computeIfHit() {
	
	// Checking if we hold a valid weapon
	p_my_weapon = p_local_player->GetActiveWeapon();
	if (!p_my_weapon)
		return false;
	
	CTraceFilter filter;
	filter.pSkip = p_local_player;
	trace_t trace;
	ray_t ray;
	ray.Init(
		point_my_position,
		point_my_position + vec_aim_direction * (p_my_weapon->GetCSWpnData()->flRange));

	g_pEnginetrace->TraceRay(ray, 0x46004003, &filter, &trace);
	
	if (!is_ennemy_valid(trace.m_pEnt))
		return false;

	switch (trace.hitbox) {
	case bones_ids::head:
		reward = 1.f;
		break;
	default:
		reward = 0.5;
	}
	return true;
}

void Capi::computeClosest() {

	float min_dist = FLT_MAX;
	
	C_BaseEntity* p_ennemy_entity;
	float dist_to_ennemy = 0.f;

	for (int ennemy_player_index = 0; ennemy_player_index < g_pEngine->GetMaxClients(); ennemy_player_index++) {

		// Checking if the considered player is different from me
		if (ennemy_player_index == my_index)
			continue;

		p_ennemy_entity = g_pEntityList->GetClientEntity(ennemy_player_index);

		if (!is_ennemy_valid(p_ennemy_entity))
			continue;
		
		// Computing distance
		Vector point_ennemy_position = p_ennemy_entity->GetEyePosition();
		Vector vec_me_to_ennemy = point_ennemy_position - point_my_position; //OE

		Vector vec_projection = vec_aim_direction * (vec_me_to_ennemy.Dot(vec_aim_direction)); // OP

		dist_to_ennemy = vec_me_to_ennemy.DistTo(vec_projection); // ||OP - OE||

		if (dist_to_ennemy < min_dist) {
			min_dist = dist_to_ennemy;
		}
	}

	// Computing reward
	//reward = 0.5 * exp(- min_dist);
	reward = 0.5 -min_dist;
}

bool Capi::is_ennemy_valid(C_BaseEntity* ennemy_entity) {

	if (!ennemy_entity)
		return false;

	if (ennemy_entity->IsDormant())
		return false;

	if (!ennemy_entity->IsAlive())
		return false;

	int ennemy_team = ennemy_entity->GetTeam();

	if (ennemy_team != 2 && ennemy_team != 3)
		return false;

	if (ennemy_team == my_team)
		return false;

	// TODO check if aiming an immune ennemy is bad !
	if (ennemy_entity->IsImmune())
		return false;
	
	return true;
}

void Capi::sendReward() {

	//cout << "sending reward to client" << endl;

	cout << "reward = " << reward << endl;

	send(client_socket, (const char *) &reward, sizeof reward, 0);

	//cout << "reward sent to client" << endl;
}