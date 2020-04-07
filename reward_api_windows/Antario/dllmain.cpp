#include <thread>
#include "Hooks.h"
#include "Utils\Utils.h"
#include "Settings.h"
#include "Utils\DrawManager.h"
#include "AIMBOT_API\api.h"

DWORD WINAPI OnDllAttach(PVOID base)
{
    Hooks::Init();

	g_api.init();

	while (true)//g_api.bRunning)//tu peux le gerer avec une commande
	{
		using namespace std::literals::chrono_literals;
		std::this_thread::sleep_for(1s);
	}

    FreeLibraryAndExitThread(static_cast<HMODULE>(base), 1);
}

VOID WINAPI OnDllDetach()
{
#ifdef _DEBUG
    fclose((FILE*)stdin);
    fclose((FILE*)stdout);

    HWND hw_ConsoleHwnd = GetConsoleWindow();     //Get the HWND of the console.
    FreeConsole();                                //Detach the console.
    PostMessageW(hw_ConsoleHwnd, WM_CLOSE, 0, 0); //Destroys the window.
#endif
}

BOOL WINAPI DllMain(HMODULE hModule, DWORD dwReason, LPVOID lpReserved)
{
    if (dwReason == DLL_PROCESS_ATTACH) 
    {
        DisableThreadLibraryCalls(hModule);
        auto h = CreateThread(nullptr, NULL, OnDllAttach, hModule, NULL, nullptr);
        if (!h)
            throw std::exception("Error while creating thread.");

        CloseHandle(h);
    }
    else if (dwReason == DLL_PROCESS_DETACH) 
    {
        if (!lpReserved)
        {
            Hooks::Restore();
            using namespace std::literals::chrono_literals;
            std::this_thread::sleep_for(1s);
        }

        OnDllDetach();
    }
    return TRUE;
}

