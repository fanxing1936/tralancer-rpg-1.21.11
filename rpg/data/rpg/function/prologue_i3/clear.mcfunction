# 中止序章：所有在线的人还原，清场
execute as @a[tag=rpg.pri3] run function rpg:prologue_i3/iso/restore
function rpg:prologue_i3/cleanup
tellraw @s {"text":"[序章] 已中止。","color":"#E8D9B0"}
