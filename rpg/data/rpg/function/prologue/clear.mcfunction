# 中止序章：所有在线的人还原，清场
execute as @a[tag=rpg.pr] run function rpg:prologue/iso/restore
function rpg:prologue/cleanup
tellraw @s {"text":"[序章] 已中止。","color":"#E8D9B0"}
