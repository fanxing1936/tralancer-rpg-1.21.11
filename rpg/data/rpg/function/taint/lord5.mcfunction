# 萨麦尔。契约不是租约：借过的力，最后会自己来取回去。
#
# 底子与无名者那只一样：卫道士 + devil 标签（隐身与烟雾由包里
# 已有的恶魔 boss 那一套负责），最多十分钟后自己散掉。
summon minecraft:vindicator ~ ~1 ~ {Tags:["rpg.advent","rpg.demon","devil","rpg.advent.new","rpg.health700"],Johnny:1,Silent:1b,PersistenceRequired:1b,CustomName:[{"text":"[DEVIL]","color":"#7B241C","bold":true,"italic":false},{"text":"萨麦尔","color":"#7B241C","italic":false}],Health:700f,active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b},{id:"speed",duration:-1,amplifier:1,show_particles:0b}],attributes:[{id:"max_health",base:700f},{id:"attack_damage",base:11f},{id:"attack_knockback",base:2f},{id:"armor",base:8f},{id:"follow_range",base:48f},{id:"knockback_resistance",base:0.5f}],drop_chances:{mainhand:0f},Passengers:[{id:"minecraft:marker",Tags:["rpg.demon.soul"]}]}
# 记下他是哪一位 —— 出手时按这个分流。要在 advent_life 之前，
# 那一步会把 rpg.advent.new 摘掉。
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.advent.new] rpg_dm_lord 5
function rpg:taint/advent_life
particle dust{color:[0.48,0.14,0.11],scale:3} ~ ~1.2 ~ 0.8 1 0.8 0.05 70
playsound minecraft:entity.evoker.cast_spell hostile @a[distance=..48] ~ ~ ~ 1 0.5
