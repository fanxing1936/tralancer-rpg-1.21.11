
# 只在真正掷中召唤技时统计；附近最多保留六只一阶段侍从。
scoreboard players set #boss_minions rpg_boss_fx 0
execute as @e[tag=devil,tag=!boss,distance=..24] run scoreboard players add #boss_minions rpg_boss_fx 1
execute if score #boss_minions rpg_boss_fx matches ..5 at @a[distance=..20,limit=1,sort=random] run playsound minecraft:entity.ghast.hurt player @a[distance=..15]
execute if score #boss_minions rpg_boss_fx matches ..5 at @a[distance=..20,limit=1,sort=random] run summon vindicator ~ ~ ~ {Johnny:1,Health:50,Silent:1b,Tags:["devil","rpg.boss.minion"],active_effects:[{id:speed,duration:-1,amplifier:1,show_particles:0b}],attributes:[{id:attack_knockback,base:2f},{id:"max_health",base:100f}]}
