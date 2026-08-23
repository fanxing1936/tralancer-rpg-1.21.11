# 从这个人身上挣出来的是谁 —— 看他签的是哪一柱。
# 没签过的人交给最后那一行的无名者。
execute if score #lord rpg_fall matches 1 run return run function rpg:taint/lord1
execute if score #lord rpg_fall matches 2 run return run function rpg:taint/lord2
execute if score #lord rpg_fall matches 3 run return run function rpg:taint/lord3
execute if score #lord rpg_fall matches 4 run return run function rpg:taint/lord4
execute if score #lord rpg_fall matches 5 run return run function rpg:taint/lord5
execute if score #lord rpg_fall matches 6 run return run function rpg:taint/lord6
execute if score #lord rpg_fall matches 7 run return run function rpg:taint/lord7
summon minecraft:vindicator ~ ~1 ~ {Tags:["rpg.advent","rpg.demon","devil","rpg.advent.new"],Johnny:1,Silent:1b,PersistenceRequired:1b,CustomName:[{"text":"[DEVIL]","color":"#3D0000","bold":true,"italic":false},{"text":"无名者","color":"dark_gray","italic":false}],Health:120f,active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b},{id:"speed",duration:-1,amplifier:1,show_particles:0b}],attributes:[{id:"max_health",base:120f},{id:"attack_damage",base:11f},{id:"attack_knockback",base:2f},{id:"armor",base:8f},{id:"follow_range",base:48f},{id:"knockback_resistance",base:0.5f}],drop_chances:{mainhand:0f}}
function rpg:taint/advent_life
