execute unless data storage rpg:forge it[0] run return 0
data modify storage rpg:forge cur set from storage rpg:forge it[0]
execute if data storage rpg:forge cur{type:"minecraft:armor",operation:"add_value"} unless data storage rpg:forge cur{id:"rpg:forge/bonus"} unless data storage rpg:forge cur{slot:"mainhand"} unless data storage rpg:forge cur{slot:"offhand"} unless data storage rpg:forge cur{slot:"hand"} run function rpg:forge/base/add_b
execute if data storage rpg:forge cur{type:"minecraft:armor_toughness",operation:"add_value"} unless data storage rpg:forge cur{slot:"mainhand"} unless data storage rpg:forge cur{slot:"offhand"} unless data storage rpg:forge cur{slot:"hand"} run function rpg:forge/base/add_s
data remove storage rpg:forge it[0]
function rpg:forge/base/armor_loop
