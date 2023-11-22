-- upgrade --
ALTER TABLE `user` MODIFY COLUMN `username` INT NOT NULL  COMMENT '用户手机号';
-- downgrade --
ALTER TABLE `user` MODIFY COLUMN `username` VARCHAR(255) NOT NULL  COMMENT '用户姓名';
