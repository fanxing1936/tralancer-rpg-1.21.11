# 中止序章：所有在线的人还原，清场
execute as @a[tag=rpg.pri4] run function rpg:prologue_i4/iso/restore
function rpg:prologue_i4/cleanup
tellraw @s {"text":"[序章] 已中止。","color":"#E8D9B0"}
