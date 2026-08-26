scoreboard players operation #ch1_debug_obj rpg_ch1_obj = @s rpg_ch1_obj
execute positioned ^8 ^ ^18 run function rpg:campaign/beelzebub/spawn/minion/zepar
execute positioned ^-8 ^ ^18 run function rpg:campaign/beelzebub/spawn/minion/botis
execute positioned ^12 ^ ^26 run function rpg:campaign/beelzebub/spawn/minion/bathin
execute positioned ^-12 ^ ^26 run function rpg:campaign/beelzebub/spawn/minion/sallos
execute positioned ^ ^ ^30 run function rpg:campaign/beelzebub/spawn/minion/purson
scoreboard players operation @s rpg_ch1_obj = #ch1_debug_obj rpg_ch1_obj
