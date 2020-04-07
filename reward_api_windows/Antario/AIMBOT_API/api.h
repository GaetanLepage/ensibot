#pragma once

#include <iostream>
#include <windows.h>
#include <cmath>
#include <thread>
#include "../Utils/Interfaces.h"
#include "../SDK/IClientMode.h"
#include "../SDK/CInput.h"
#include "../SDK/CTraceFilter.h"
#include "../SDK/IEngineTrace.h"
#pragma comment(lib, "Ws2_32.lib")

using namespace std;

// This class is exported from the dll
class Capi {

private:

	// Socket servers
	SOCKET server_socket, client_socket;
	
	// Reward computation
	float reward;

	enum bones_ids {
		head = 0,
		neck = 2,

		spine_1 = 4,
		spine_2 = 5,
		spine_3 = 6,
		spine_4 = 7,

		left_upper_arm = 18,
		left_forearm = 19,
		left_and = 15,

		right_upper_arm = 16,
		right_forearm = 17,
		right_and = 14,

		left_thigh = 9,
		left_calf = 11,
		left_foot = 13,

		right_thigh = 8,
		right_calf = 10,
		right_foot = 12,
	};

	CUserCmd* p_cmd;

	C_BaseEntity* p_local_player;
	int my_index;
	int my_team;
	C_BaseCombatWeapon* p_my_weapon;
	Vector point_my_position;
	QAngle my_view_angles;
	Vector vec_aim_direction;

public:

	Capi(void);

	void init();

	~Capi() {}


	// SOCKET UTILITIES

	bool is_client_connected;

	void createConsole();

	void createServer();

	SOCKET get_client_socket();

	void handleMessage(string message);

	// REWARD

	void computeReward(CUserCmd* pCmd);

	bool computeIfHit();

	void computeClosest();

	bool is_ennemy_valid(C_BaseEntity* ennemy_entity);

	void sendReward();
};


extern Capi g_api;


