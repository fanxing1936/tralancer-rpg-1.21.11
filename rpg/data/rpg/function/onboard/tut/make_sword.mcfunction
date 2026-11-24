# 照 rpg:forge/smelt/make 炼一件长剑（不弹出物品，直接放进玩家的格子）
function rpg:forge/wb/new
execute store result score #r rpg_fg run random value 0..7
execute store result storage rpg:forge nm.r int 1 run scoreboard players get #r rpg_fg
function rpg:forge/smelt/prefix with storage rpg:forge nm
scoreboard players set #souls rpg_fg 1
scoreboard players set #best rpg_fg -100
function rpg:forge/smelt/roll
scoreboard players operation #q0 rpg_fg = #best rpg_fg
function rpg:onboard/tut/m_sword with storage rpg:forge nm
execute as @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] run function rpg:forge/init
function rpg:forge/wb/save_off
function rpg:forge/wb/close
