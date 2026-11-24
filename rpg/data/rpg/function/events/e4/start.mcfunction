function rpg:events/place_near
function rpg:events/e4/begin
execute at @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] run summon minecraft:rabbit ~ ~ ~ {Tags:["rpg.ev.gob"],RabbitType:1,PersistenceRequired:1b,CustomNameVisible:1b,CustomName:["",{"text":"𝔗𝔯𝔢𝔞𝔰𝔲𝔯𝔢 ℜ𝔞𝔟𝔟𝔦𝔱","color":"#FFFFFF","bold":false,"italic":false}],attributes:[{id:"scale",base:1.4d},{id:"movement_speed",base:0.45d},{id:"max_health",base:12d}],Health:12f,active_effects:[{id:"glowing",duration:-1,amplifier:0,show_particles:0b}]}
tellraw @a[distance=..64] ["",{"text":"〖事件・寻宝者〗","color":"#FFD85A","bold":true,"italic":false},{"text":" 𝔗𝔯𝔢𝔞𝔰𝔲𝔯𝔢 ℜ𝔞𝔟𝔟𝔦𝔱","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"一只背着钱袋的兔子在附近乱跑，30 秒后就跑没了。","color":"#9C9A94","bold":false,"italic":false}]
playsound minecraft:entity.rabbit.jump master @a[distance=..64] ~ ~ ~ 1 0.6
