scoreboard players operation #dx rpg_xb = #mx rpg_xb
$scoreboard players operation #dx rpg_xb -= #x$(i) rpg_tw
scoreboard players operation #dz rpg_xb = #mz rpg_xb
$scoreboard players operation #dz rpg_xb -= #z$(i) rpg_tw
scoreboard players operation #dx rpg_xb *= #dx rpg_xb
scoreboard players operation #dz rpg_xb *= #dz rpg_xb
scoreboard players operation #dx rpg_xb += #dz rpg_xb
scoreboard players operation #best rpg_xb < #dx rpg_xb
