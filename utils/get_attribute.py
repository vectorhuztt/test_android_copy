#!/usr/bin/env python
# encoding:UTF-8  
# @Author  : SUN FEIFEI


class GetAttribute:
    """获取元素属性"""

    @classmethod
    def get_class_name(cls, var):
        """元素 class_name属性值"""
        value = var.get_attribute("className")
        return value

    @classmethod
    def get_resource_id(cls, var):
        """元素 resource-id属性值"""
        value = var.get_attribute("resourceId")
        return value

    @classmethod
    def get_selected(cls, var):
        """元素 selected属性值"""
        value = var.get_attribute('selected')
        return value

    @classmethod
    def get_checked(cls, var):
        """元素 checked属性值"""
        value = var.get_attribute('checked')
        return value

    @classmethod
    def get_enabled(cls, var):
        """元素 enabled属性值"""
        value = var.get_attribute('enabled')
        return value

    @classmethod
    def get_cont_desc(cls, var):
        value = var.get_attribute('contentDescription')
        return value
