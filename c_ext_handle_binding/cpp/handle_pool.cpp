#include "handle_pool.hpp"

HandleId HandlePool::store(std::unique_ptr<HandleObject> obj) {
    const HandleId id = next_id_++;
    handles_[id] = std::move(obj);
    return id;
}

HandleObject* HandlePool::get(HandleId handle) {
    auto it = handles_.find(handle);
    if (it == handles_.end()) {
        return nullptr;
    }
    return it->second.get();
}

bool HandlePool::release(HandleId handle) {
    return handles_.erase(handle) > 0;
}

int HandlePool::type_of(HandleId handle) const {
    auto it = handles_.find(handle);
    if (it == handles_.end()) {
        return kInvalidTypeId;
    }
    return static_cast<int>(it->second->type());
}
