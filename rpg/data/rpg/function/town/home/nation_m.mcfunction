# 宏：玩家的国家（rpg:onboard p<id>.nation）→ #nat
$data modify storage rpg:town n set value "$(nation)"
scoreboard players set #nat rpg_tw -1
execute if data storage rpg:town {n:"犹大王国"} run scoreboard players set #nat rpg_tw 0
execute if data storage rpg:town {n:"以色列北国"} run scoreboard players set #nat rpg_tw 1
execute if data storage rpg:town {n:"以东公国"} run scoreboard players set #nat rpg_tw 2
execute if data storage rpg:town {n:"摩押王国"} run scoreboard players set #nat rpg_tw 3
execute if data storage rpg:town {n:"亚扪联邦"} run scoreboard players set #nat rpg_tw 4
execute if data storage rpg:town {n:"非利士五城同盟"} run scoreboard players set #nat rpg_tw 5
execute if data storage rpg:town {n:"亚兰帝国"} run scoreboard players set #nat rpg_tw 6
execute if data storage rpg:town {n:"推罗海商共和国"} run scoreboard players set #nat rpg_tw 7
execute if data storage rpg:town {n:"基列边境领"} run scoreboard players set #nat rpg_tw 8
execute if data storage rpg:town {n:"圣城教廷领"} run scoreboard players set #nat rpg_tw 9
