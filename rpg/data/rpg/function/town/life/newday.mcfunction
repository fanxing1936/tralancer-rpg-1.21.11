# 新的现实日：#lastday 跟上；每个人的「今天」在用到时再比（rpg_tl_d、rpg_tl_qd*）
scoreboard players operation #lastday rpg_tl = #day rpg_tl
scoreboard players operation #day1 rpg_tl = #day rpg_tl
scoreboard players add #day1 rpg_tl 1
function #rpg:town_newday
