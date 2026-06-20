#pragma once

#include "handle_object.hpp"

#include <memory>
#include <unordered_map>

class HandlePool {
public:
    HandleId store(std::unique_ptr<HandleObject> obj);
    HandleObject* get(HandleId handle);
    bool release(HandleId handle);
    int type_of(HandleId handle) const;

    template <typename T>
    T* get_as(HandleId handle, TypeId expected) {
        HandleObject* obj = get(handle);
        if (obj == nullptr || obj->type() != expected) {
            return nullptr;
        }
        return static_cast<T*>(obj);
    }

private:
    HandleId next_id_ = 1;
    std::unordered_map<HandleId, std::unique_ptr<HandleObject>> handles_;
};
