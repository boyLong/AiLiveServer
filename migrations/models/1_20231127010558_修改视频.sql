-- upgrade --
ALTER TABLE `Reply_Tag` DROP FOREIGN KEY `fk_Reply_Ta_group_ce73ce49`;
ALTER TABLE `Reply_Tag` CHANGE group_id_id group_id INT;
ALTER TABLE `Reply_Tag` ADD CONSTRAINT `fk_Reply_Ta_group_b2274991` FOREIGN KEY (`group_id`) REFERENCES `group` (`id`) ON DELETE CASCADE;
-- downgrade --
ALTER TABLE `Reply_Tag` DROP FOREIGN KEY `fk_Reply_Ta_group_b2274991`;
ALTER TABLE `Reply_Tag` CHANGE group_id group_id_id INT;
ALTER TABLE `Reply_Tag` ADD CONSTRAINT `fk_Reply_Ta_group_ce73ce49` FOREIGN KEY (`group_id_id`) REFERENCES `group` (`id`) ON DELETE CASCADE;
